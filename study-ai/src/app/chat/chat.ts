import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-chat',
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.html',
  styleUrls: ['./chat.css'],
})
export class Chat {
  chapters = ['Banking', 'Circle'];
  selectedChapter = 'Banking';
  userInput = '';
  messages: { role: 'user' | 'ai'; text: string }[] = [];
  uploadedFiles: { [key: string]: boolean } = {};
  selectedQuestionImage: File | null = null;

  sendMessage() {
    if (!this.userInput.trim() && !this.selectedQuestionImage) return;

    // Show user input or image message
    if (this.userInput.trim()) {
      this.messages.push({ role: 'user', text: this.userInput.trim() });
      this.messages.push({
        role: 'ai',
        text: `AI reply to "${this.userInput.trim()}"`,
      });
    }

    if (this.selectedQuestionImage) {
      this.messages.push({
        role: 'user',
        text: `📷 Uploaded question image: ${this.selectedQuestionImage.name}`,
      });

      // Simulated backend OCR reply
      this.messages.push({
        role: 'ai',
        text: `🧠 AI answer to question from uploaded image.`,
      });

      this.selectedQuestionImage = null; // Reset after processing
    }

    this.userInput = '';
  }

  handleEnter(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      event.preventDefault();
      this.sendMessage();
    }
  }

  selectChapter(ch: string) {
    this.selectedChapter = ch;
    this.messages = [];
  }

  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
      this.uploadedFiles[this.selectedChapter] = true;
    }
  }

  onQuestionImageSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
      this.selectedQuestionImage = file;
    }
  }
}
