import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-home',
  imports: [ReactiveFormsModule, FormsModule, CommonModule],
  templateUrl: './home.html',
  styleUrls: ['./home.css'],
})
export class Home {
  sessionForm: FormGroup;
  chapters: string[] = ['Banking', 'Finance', 'Technology', 'Education'];

  constructor(private fb: FormBuilder, private router: Router) {
    this.sessionForm = this.fb.group({
      name: ['', Validators.required],
      mobile: [
        '',
        [
          Validators.required,
          Validators.pattern('^[0-9]{10}$'),
          Validators.minLength(10),
          Validators.maxLength(10),
        ],
      ],
      chapter: [this.chapters[0], Validators.required],
    });
  }

  onSubmit() {
    if (this.sessionForm.valid) {
      // Example: Navigate to chat or emit session info
      // this.router.navigate(['/chat'], { queryParams: this.sessionForm.value });
      console.log(this.sessionForm.value);
      // Optionally: show a success message or transition
    } else {
      // Touch all controls for error feedback
      Object.values(this.sessionForm.controls).forEach((control) =>
        control.markAsTouched()
      );
    }
  }
}
