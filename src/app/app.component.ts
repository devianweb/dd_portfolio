import { DOCUMENT } from '@angular/common';
import { Component, ElementRef, Inject, ViewChild } from '@angular/core';
import { ChildrenOutletContexts } from '@angular/router';
import { EasingLogic, PageScrollService } from 'ngx-page-scroll-core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'dd_portfolio';

  constructor(
    private pageScrollService: PageScrollService,
    @Inject(DOCUMENT) private document: any
  ) {}

  public scroll(id: string): void {
    this.pageScrollService.scroll({
      document: this.document,
      scrollTarget: id,
      easingLogic: this.defaultEasing,
    });
  }

  public defaultEasing: EasingLogic = (
    t: number,
    b: number,
    c: number,
    d: number
  ): number => {
    if (t === 0) {
      return b;
    }
    if (t === d) {
      return b + c;
    }
    if ((t /= d / 2) < 1) {
      return (c / 2) * Math.pow(2, 10 * (t - 1)) + b;
    }

    return (c / 2) * (-Math.pow(2, -10 * --t) + 2) + b;
  };
}
