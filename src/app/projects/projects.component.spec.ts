import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectsComponent } from './projects.component';

describe('ProjectsComponent', () => {
  let fixture: ComponentFixture<ProjectsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ProjectsComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(ProjectsComponent);
    fixture.detectChanges();
  });

  it('shows SkirmishLab first, linking out in a new tab with its disclaimer', () => {
    const card = (fixture.nativeElement as HTMLElement).querySelector(
      '.card'
    ) as HTMLAnchorElement;
    expect(card.querySelector('.card-title')?.textContent).toContain('SkirmishLab');
    expect(card.href).toContain('https://skirmishlab.duskwood.design');
    expect(card.target).toBe('_blank');
    expect(card.rel).toContain('noopener');
    expect(card.textContent).toContain('unofficial fan project');
  });
});
