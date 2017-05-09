import { Component } from '@angular/core';
import {enableProdMode} from '@angular/core';

enableProdMode();

import { headerComponent } from './modules/header/app.headerComponent';
import { navComponent } from './modules/nav/app.navComponent';
import { footerComponent } from './modules/footer/app.footerComponent';

import { homeComponent } from './views/home/app.homeComponent';
import { contentAreaComponent } from './views/contentArea/app.contentAreaComponent';
import { contactComponent } from './views/contact/app.contactComponent';
import { aboutComponent } from './views/about/app.aboutComponent';
import { loaderComponent } from './views/loader/app.loaderComponent';



@Component({
  selector: 'app-root',
  templateUrl: './app.main.html',
 })

export class AppComponent {


}
//  title = ' Welcome Ricardo!';
