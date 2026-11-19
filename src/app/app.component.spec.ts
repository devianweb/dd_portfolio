import { TestBed } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { ProjectsComponent } from './projects/projects.component';
import { SocialListComponent } from './social-list/social-list.component';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [
        AppComponent,
        LandingPageComponent,
        ProjectsComponent,
        SocialListComponent,
      ],
    }).compileComponents();
  });

  it('renders the home and projects sections', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.querySelector('#home')).toBeTruthy();
    expect(el.querySelector('#projects')).toBeTruthy();
    expect(el.querySelector('#about')).toBeNull();
  });
});
