import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ContributersComponent } from './contributers.component';

describe('ContributersComponent', () => {
  let component: ContributersComponent;
  let fixture: ComponentFixture<ContributersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ContributersComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ContributersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
