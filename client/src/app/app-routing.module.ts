import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ContentComponent } from './content/content.component';
import { ContributersComponent } from './contributers/contributers.component';
import { AboutComponent } from './about/about.component';
import { SamplesComponent } from './samples/samples.component';

const routes: Routes = [
  {path : '', component : ContentComponent},
  {path : 'dashboard', component : ContentComponent},
  {path : 'contributer', component : ContributersComponent},
  {path : 'about', component : AboutComponent},
  {path : 'samples', component : SamplesComponent},

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
