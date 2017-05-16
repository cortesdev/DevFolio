//custom-transition.animation.ts
import {trigger, state, animate, style, transition, AnimationEntryMetadata} from '@angular/core';

export function customTransition():AnimationEntryMetadata {
 return slideOutAndIn();
}

function slideOutAndIn():AnimationEntryMetadata {
 return trigger('ng2ElementState', [
   state('leave', style({
       position:'fixed',
       width:'100%'
   })),
   state('enter', style({
       position:'fixed',
       width:'100%'
   })),
   transition('* => enter', [
       style({transform: 'translateX(100%)'}),
       animate('0.5s ease-in-out', style({transform: 'translateX(0%)'}))
   ]),
   transition('* => leave', [
     style({transform: 'translateX(0%)'}),
     animate('0.5s ease-in-out', style({transform: 'translateX(-100%)'}))
   ]),
 ]);
}
