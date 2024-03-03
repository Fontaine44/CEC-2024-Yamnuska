import { ChangeDetectorRef, Component} from '@angular/core';
import data from './search_space.json';
import path1 from './firstRigPath.json';
import path2 from './secondRigPath.json';

@Component({
  selector: 'app-form',
  templateUrl: './example1.component.html',
  styleUrls: ['./example1.component.scss']
})
export class Example1Component {

  // Init the paths
  path1: any = path1;
  path2: any = path2;

  view: number = 28;                        // Number of squares on the sides of the rigs
  tileSize: number = 500/(this.view*2+1);   // Tile size in pixels used

  // Starting positions of the rigs
  rig1Position: number[] = [parseInt(path1[0][0]), parseInt(path1[0][1])];
  rig2Position: number[] = [parseInt(path2[0][0]), parseInt(path2[0][1])];

  // Current day (0-29) and rig (0 or 1)
  currentDay: number = 0;
  currentRig: number = 0;

  isPlaying: boolean = false;   // True if the animation is playing
  slowMode: boolean = false;    // True if slow-mo mode is enabled
  grid: string[][] = [];        // Holds the current grid values
  opacity: number[][] = [];     // Holds the current grid opacities

  updateInterval: number = 1000                     // Time between days in ms
  gridUpdateInterval: NodeJS.Timeout | undefined;   // Timeout to update the grid at a current interval

  constructor(private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.showGrid();    // Show initial grid
  }

  showGrid() {
    // Get the ranges of the grid depending on the position of the tracked rig
    let gridRangeX;
    let gridRangeY;

    if (this.currentRig == 0) {
      gridRangeX = this.getGridRange(this.rig1Position[0]);
      gridRangeY = this.getGridRange(this.rig1Position[1]);
    } else {
      gridRangeX = this.getGridRange(this.rig2Position[0]);
      gridRangeY = this.getGridRange(this.rig2Position[1]);
    }

    // Reset the arrays
    this.grid = [];
    this.opacity = [];

    // Init the sub-arrays
    for (let col = 0; col <= gridRangeY[1] - gridRangeY[0] + 1; col++) {
      this.grid[col] = [];
      this.opacity[col] = [];
    }

    // Initialize the grid with land and water
    for (let col = 0; col <= gridRangeY[1] - gridRangeY[0] + 1; col++) {
      let yPos = gridRangeY[0] + col;
      for (let row = 0; row <= gridRangeX[1] - gridRangeX[0] + 1; row++) {
        let xPos = gridRangeX[0] + row;

        // Set base the opacity for each grid cell
        this.opacity[col][row] = 1;

        // Set the type of cell and the opacity
        if (yPos == this.rig1Position[1] && xPos == this.rig1Position[0]) {
          this.grid[col][row] = 'player';
        } else if (yPos == this.rig2Position[1] && xPos == this.rig2Position[0]) {
          this.grid[col][row] = 'player';
        } else if (data[xPos][yPos][this.currentDay][0] == 0.0) {
          this.grid[col][row] = 'water';
          this.opacity[col][row] = data[xPos][yPos][this.currentDay][1];
        } else {
          this.grid[col][row] = 'land';
        }
      }
    }
  }

  // Determine the range of the grid to show
  getGridRange(pos: number): number[] {
    if (pos+this.view> 99) {
      return [99-this.view*2, 99];
    } else if (pos-this.view< 0) {
      return [0, this.view*2];
    } else {
      return [pos-this.view, pos+this.view];
      } 
    }

  // Start the periodic update of the animation
  startGridUpdate() {
    if (this.isPlaying) {
      return; // Grid update is already in progress
    }

    this.isPlaying = true;
    this.gridUpdateInterval = setInterval(() => {
      this.updateGridBasedOnMove();
    }, this.updateInterval);
  }

  // Stop the periodic update of the animation
  stopGridUpdate() {
    if (!this.isPlaying) {
      return; // Grid update is not active
    }

    this.isPlaying = false;
    clearInterval(this.gridUpdateInterval);
  }


  updateGridBasedOnMove() {
    if (this.currentDay < path1.length) {

      // set the positions of the rigs
      this.rig1Position = path1[this.currentDay];
      this.rig2Position = path2[this.currentDay];

      this.currentDay++;    // Go to the next day

      // Rerender the grid
      this.showGrid();
      this.cdr.detectChanges();

    } else {
      // Reset the day if all days are completed
      this.currentDay = 0;
      this.updateGridBasedOnMove();
    }
  }

  // Reset the animation to day 0
  resetAnimation() {
    this.currentDay = 0;
    if (!this.isPlaying) {
      return; // Grid update is not active
    }

    this.isPlaying = false;
    clearInterval(this.gridUpdateInterval);
  }

  // Changes the current rig tracked
  changeRig() {
    if (this.currentRig == 1) {
      this.currentRig = 0;
    } else {
      this.currentRig = 1;
    }
  }

  // Changes the updateInterval based on the slow-mo mode
  onSwitchChange() {
    this.stopGridUpdate();
    if (this.slowMode) {
      this.updateInterval = 2000;
    } else {
      this.updateInterval = 1000;
    }
    this.startGridUpdate();
  }
}
