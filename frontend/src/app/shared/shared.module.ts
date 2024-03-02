import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AppRoutingModule } from '../app-routing.module';
import { NavbarComponent } from './components/navbar/navbar.component';
import { GridCellComponent } from './components/grid-cell/grid-cell.component';



@NgModule({
  declarations: [
    NavbarComponent,
    GridCellComponent
  ],
  imports: [
    CommonModule,
    AppRoutingModule
  ],
  exports : [
    NavbarComponent,
    GridCellComponent
  ]
})
export class SharedModule { }
