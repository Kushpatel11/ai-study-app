// Main routing configuration for the Angular app.

import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Chat } from './chat/chat';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'chat', component: Chat },
  // Optionally, handle unknown routes:
  { path: '**', redirectTo: '', pathMatch: 'full' },
];
