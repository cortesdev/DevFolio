import { animate, AnimationEntryMetadata, state, style, transition, trigger } from '@angular/core';

// Component transition animations
export const slideInDownAnimation: AnimationEntryMetadata =
  trigger('routeAnimation', [
    state('*',
      style({
        opacity: 1,
        transform: 'translateX(0)'
      })
    ),
    transition(':enter', [
      style({
        opacity: 0,
        transform: 'translateX(-100%)'
      }),
      animate('0.2s ease-in')
    ]),
    transition(':leave', [
      animate('0.5s ease-out', style({
        opacity: 0,
        transform: 'translateY(100%)'
      }))
    ])
  ]);


  export function routerTransition() {
    return slideToLeft();
  }

  function slideToLeft() {
    return trigger('routerTransition', [
      state('void', style({position:'fixed', width:'100%'}) ),
      state('*', style({position:'fixed', width:'100%'}) ),
      transition(':enter', [  // before 2.1: transition('void => *', [
        style({transform: 'translateX(100%)'}),
        animate('0.5s ease-in-out', style({transform: 'translateX(0%)'}))
      ]),
      transition(':leave', [  // before 2.1: transition('* => void', [
        style({transform: 'translateX(0%)'}),
        animate('0.5s ease-in-out', style({transform: 'translateX(-100%)'}))
      ])
    ]);
  }
