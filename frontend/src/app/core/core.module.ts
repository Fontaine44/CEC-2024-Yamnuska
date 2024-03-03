import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { PlotlyModule } from 'angular-plotly.js';
import { SharedModule } from 'app/shared/shared.module';
import { CustomComponent } from './components/custom/custom.component';
import { Example1Component } from './components/example1/example1.component';


const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'example',
    component: Example1Component,
  },
  {
    path: 'custom',
    component: CustomComponent,
  }
];


@NgModule({
  declarations: [
    HomeComponent,
    Example1Component,
    CustomComponent,
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    SharedModule,
    ReactiveFormsModule,
    PlotlyModule,
    FormsModule
  ],
  exports: [
    RouterModule
  ]
})
export class CoreModule { }
