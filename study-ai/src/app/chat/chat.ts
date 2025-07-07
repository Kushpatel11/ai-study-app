import { Component, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface Message {
  role: 'user' | 'ai';
  text: string;
}

interface Chapter {
  name: string;
  hasMaterial: boolean;
}

@Component({
  standalone: true,
  selector: 'app-chat',
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.html',
  styleUrls: ['./chat.css'],
})
export class Chat {
  chapters: Chapter[] = [
    { name: 'Banking', hasMaterial: false },
    { name: 'Circle', hasMaterial: false },
    // Add more chapters as needed
  ];
  selectedChapter: Chapter | null = this.chapters[0];
  messages: Message[] = [];
  userInput = '';

  @ViewChild('chatScroll') chatScroll!: ElementRef<HTMLDivElement>;

  selectChapter(chapter: Chapter) {
    this.selectedChapter = chapter;
    this.messages = [];
  }

  sendMessage() {
    if (!this.userInput.trim() || !this.selectedChapter?.hasMaterial) return;
    const text = this.userInput.trim();
    this.messages.push({ role: 'user', text });
    // Example: Replace with real API call
    setTimeout(() => {
      this.messages.push({
        role: 'ai',
        text: `AI Response to: "${text}" for ${this.selectedChapter?.name}`,
      });
      this.scrollToBottom();
    }, 600);
    this.userInput = '';
    this.scrollToBottom();
  }

  handleEnter(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file || !this.selectedChapter) return;
    // TODO: Upload file to backend and set hasMaterial true on success
    // Example: Simulate upload
    setTimeout(() => {
      this.selectedChapter!.hasMaterial = true;
    }, 800);
  }

  requestSummary() {
    if (!this.selectedChapter?.hasMaterial) return;
    // TODO: Replace with API call
    this.messages.push({
      role: 'ai',
      text: `Summary for ${this.selectedChapter.name}...`,
    });
    this.scrollToBottom();
  }

  requestMockTest() {
    if (!this.selectedChapter?.hasMaterial) return;
    // TODO: Replace with API call
    this.messages.push({
      role: 'ai',
      text: `Mock test for ${this.selectedChapter.name}...`,
    });
    this.scrollToBottom();
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom() {
    try {
      this.chatScroll?.nativeElement.scrollTo({
        top: this.chatScroll.nativeElement.scrollHeight,
        behavior: 'smooth',
      });
    } catch {}
  }
}
