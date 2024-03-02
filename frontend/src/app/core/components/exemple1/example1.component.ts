import { ChangeDetectorRef, Component, ElementRef, ViewChild } from '@angular/core';
import data from './search_space.json';

@Component({
  selector: 'app-form',
  templateUrl: './example1.component.html',
  styleUrls: ['./example1.component.scss']
})
export class Example1Component {

  view = 24;  // Number of squares on the sides of the rigs
  rig1Position = [21, 54];
  rig2Position = [0, 2];
  rig1Moves = [[[21,55], [21,56], [22,56]], [[22,57], [23,58], [24,59]], [[23,58], [22,57], [22,56]], [[28,55]]];
  currentDayMoveIndex = 0;
  currentDay = 0;
  tileSize = 10;
  grid: string[][] = [];
  opacity: number[][] = [];

  constructor(private cdr: ChangeDetectorRef) {
    
  }

  ngOnInit() {
    this.showGrid();
    this.startGridUpdate();
  }

  showGrid() {
    // Get the ranges of the grid
    let gridRangeX = this.getGridRange(this.rig1Position[0]);
    let gridRangeY = this.getGridRange(this.rig1Position[1]);
    console.log(gridRangeY, gridRangeX);

    this.grid = [];
    this.opacity = [];

    for (let col = 0; col <= gridRangeY[1] - gridRangeY[0] + 1; col++) {
      this.grid[col] = [];
      this.opacity[col] = [];
    }

    // Initialize the grid with land and water
    for (let col = 0; col <= gridRangeY[1] - gridRangeY[0] + 1; col++) {
      let yPos = gridRangeY[0] + col;
      for (let row = 0; row <= gridRangeX[1] - gridRangeX[0] + 1; row++) {
        let xPos = gridRangeX[0] + row;

        // Set the opacity for each grid cell
        this.opacity[col][row] = 1;

        // Set the type of cell
        if (yPos == this.rig1Position[1] && xPos == this.rig1Position[0]) {
          this.grid[col][row] = 'player';
        } else if (yPos == this.rig2Position[1] && xPos == this.rig2Position[0]) {
          this.grid[col][row] = 'player';
        } else if (parseInt(data[yPos][xPos][0]) == 0) {
          this.grid[col][row] = 'water';
          this.opacity[col][row] = 0.8;
        } else {
          this.grid[col][row] = 'land';
        }
      }
    }
  }

  // Determine the range of the grid to show
  getGridRange(pos: number): number[] {
    if (pos+this.view
    > 99) {
      return [99-this.view
    *2, 99];
    } else if (pos-this.view
    < 0) {
      return [0, this.view
    *2];
    } else {
      return [pos-this.view
    , pos+this.view
  ];
      } 
    }

  rerenderGrid() {
    this.showGrid();
    this.cdr.detectChanges();
  }

  startGridUpdate() {
    setInterval(() => {
      this.updateGridBasedOnMove();
    }, 1000);
  }

  updateRig1Position(pos: number[]) {
    this.rig1Position = pos;
  }

  updateGridBasedOnMove() {
    if (this.currentDay < this.rig1Moves.length) {
      console.log("Day: " + this.currentDay);
      console.log("Move Index: " + this.currentDayMoveIndex);
      console.log("MOves in that day: " + this.rig1Moves[this.currentDay].length);

      if (this.currentDayMoveIndex >= this.rig1Moves[this.currentDay].length) {
        this.currentDayMoveIndex = 0;
        this.currentDay++;
      } else {
        this.rig1Position = this.rig1Moves[this.currentDay][this.currentDayMoveIndex];

        this.currentDayMoveIndex++;
  
        // Rerender the grid
        this.showGrid();
        this.cdr.detectChanges();
        
        console.log("Moving to " + this.rig1Position);
      }
    } else {
      // Reset the moves if all moves are completed
      this.currentDay = 0;
      this.currentDayMoveIndex = 0;
      this.updateGridBasedOnMove();
    }
  }

}
