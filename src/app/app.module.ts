import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { ProjectsComponent } from './projects/projects.component';
import { SocialListComponent } from './social-list/social-list.component';

@NgModule({
  declarations: [
    AppComponent,
    LandingPageComponent,
    ProjectsComponent,
    SocialListComponent,
  ],
  imports: [BrowserModule],
  bootstrap: [AppComponent],
})
export class AppModule {}
