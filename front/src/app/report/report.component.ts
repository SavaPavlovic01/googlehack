import { Component, OnInit } from '@angular/core';
import {
  AfterViewInit,
  ElementRef,
  OnDestroy,
  ViewChild,
  inject,
} from '@angular/core';
import { FormGroup, FormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { MatRadioChange } from '@angular/material/radio';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { NgIf } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { CommonModule } from '@angular/common';
import * as fs from 'fs';
import * as path from 'path';
import * as dotenv from 'dotenv';
import * as mimetypes from 'mime-types';
import { TextUploadServiceService } from '../text-upload-service.service';
import { VideoUploadServiceService } from '../video-upload-service.service';
import { ImageUploadServiceService } from '../image-upload-service.service';
import { TwitterUploadServiceService } from '../twitter-upload-service.service';
import { YoutubeUploadServiceService } from '../youtube-upload-service.service';
import { F } from '@angular/cdk/a11y-module.d-DBHGyKoh';

@Component({
  selector: 'app-report',
  imports: [
    MatRadioModule,
    FormsModule,
    ReactiveFormsModule,
    NgIf,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    CommonModule
  ],
  templateUrl: './report.component.html',
  styleUrl: './report.component.css',
})
export class ReportComponent implements OnInit {

  reportForm!: FormGroup;
  result:any = null;
  selectedInput: string = '0';
  inputString: string = '';
  ytString: string = '';
  twitterString: string = '';

  base64Image: string = '';
  imageFile: File = new File([''], 'empty.png', { type: 'image/png' });

  base64Video: string = '';
  videoFile: File = new File([''], 'empty.mp4', { type: 'video/mp4' });

  imagePreview: string | ArrayBuffer | null = null;
  videoPreview: string | ArrayBuffer | null = null;

  isloading:boolean = false

  private textUploadService = inject(TextUploadServiceService);
  private videoUploadService = inject(VideoUploadServiceService);
  private imageUploadService = inject(ImageUploadServiceService);
  private twitterUploadService = inject(TwitterUploadServiceService);
  private youtubeUploadService = inject(YoutubeUploadServiceService);

  castNumberToDesc(number:string){
    switch(number) {
      case '0':
        return "Čist tekst"
      case '1':
        return "Link za youtube post"
      case '2':
        return "Link za twitter post"
      case '3':
        return "Postavljanje videa"
      case '4':
        return "Postavljanje slike"
      default:
        return ""
    }
  }
  ngOnInit(): void {
    // Initialize the FormGroup with the form controls when the component starts
    this.reportForm = new FormGroup({
      // Define the 'textField' FormControl with an initial value
      textInputString: new FormControl(''),
      youtubeLink: new FormControl(''),
      twitterLink: new FormControl(''),
      videoUpload: new FormControl(''),
      imageUpload: new FormControl(''),
      // Add other form controls here if needed
    });

    this.reportForm.get('textInputString')?.valueChanges.subscribe((value) => {
      console.log('textField value changed:', value);
      this.inputString = value;
    });
    this.reportForm.get('youtubeLink')?.valueChanges.subscribe((value) => {
      console.log('textField value changed:', value);
      this.ytString = value;
    });
    this.reportForm.get('twitterLink')?.valueChanges.subscribe((value) => {
      console.log('textField value changed:', value);
      this.twitterString = value;
    });
    this.reportForm.get('videoUpload')?.valueChanges.subscribe((value) => {
      console.log('Video value changed:', value);
    });
    this.reportForm.get('imageUpload')?.valueChanges.subscribe((value) => {
      console.log('Image value changed:', value);
    });
  }
  showFileInput: boolean = false; // Track visibility of file input

  triggerVideoUpload() {
    const videoInputEl = document.getElementById(
      'videoInput'
    ) as HTMLInputElement;
    if (videoInputEl) {
      videoInputEl.click(); // This will trigger the file input click programmatically
    } else {
      console.error('File input element not found.');
    }
  }

  triggerImageUpload() {
    const imageInputEl = document.getElementById(
      'imageInput'
    ) as HTMLInputElement;
    if (imageInputEl) {
      imageInputEl.click(); // This will trigger the file input click programmatically
    } else {
      console.error('File input element not found.');
    }
  }

  onImagePicked(event: Event) {
    const input = event.target as HTMLInputElement;

    if (input?.files?.[0]) {
      const file = input.files[0];
      this.imageFile = file;

      // const reader = new FileReader();

      // reader.onload = () => {
      //   // Save the Base64 string in the class property
      //   this.base64Image = reader.result as string;
      //   console.log(this.base64Image); // Now you have the Base64 string in 'base64Image'
      // };

      // reader.readAsDataURL(file); // Read the file as Base64
    }
    //  return;
  }
  onVideoPicked(event: Event) {
    const input = event.target as HTMLInputElement;

    if (input?.files?.[0]) {
      const file = input.files[0];
      this.videoFile = file;
    }
  }
  onRadioChange(event: MatRadioChange) {
    // The 'event' object contains information about the change.
    // 'event.value' is the value of the newly selected radio button.
    this.selectedInput = event.value; // Manually update the property

    // You can add any other logic here that should run on change
  }

  submitForm() {
    this.isloading = true;
    this.result = null
    
    console.log(this.selectedInput);

    if (this.selectedInput == '0') {
      // text
      
      this.textUploadService.uploadFile(this.inputString).subscribe({
        
        next: (response) => {
          this.isloading = false
          console.log('success', response);
          const { isHate, probability } = response;
          const confidence = Math.round(probability * 10000) / 100;
          this.result = `Ovaj sadržaj ${isHate ? 'je' : 'nije'} govor mržnje. Model je ${confidence}% siguran.`;
       
        },
        error: (err) => {
          this.isloading = false
          console.error('error', err);
          this.result = "Došlo je do greške. Pokušajte ponovo.";
        },
      });
    } else if (this.selectedInput == '1') {
      // youtube link
      this.youtubeUploadService.uploadFile(this.ytString).subscribe({
        next: (response) => {
          this.isloading = false
          console.log('success', response);
          const { isHate, probability } = response;
          const confidence = Math.round(probability * 10000) / 100;
          this.result = `Ovaj sadržaj ${isHate ? 'je' : 'nije'} govor mržnje. Model je ${confidence}% siguran.`;
        },
        error: (err) => {
          this.isloading = false
          console.error('error', err);
          this.result = "Došlo je do greške. Pokušajte ponovo.";
        },
      });
    } else if (this.selectedInput == '2') {
      // twitter link
      this.twitterUploadService.uploadFile(this.twitterString).subscribe({
        next: (response) => {
          this.isloading = false
          console.log('success', response);
          const { isHate, probability } = response;
          const confidence = Math.round(probability * 10000) / 100;
          this.result = `Ovaj sadržaj ${isHate ? 'je' : 'nije'} govor mržnje. Model je ${confidence}% siguran.`;
        },
        error: (err) => {
          this.isloading = false
          console.error('error', err);
          this.result = "Došlo je do greške. Pokušajte ponovo.";
        },
      });
    } else if (this.selectedInput == '3') {
      this.videoUploadService.uploadFile(this.videoFile).subscribe({
        next: (response) => {
          this.isloading = false
          console.log('success', response);
          const { isHate, probability } = response;
          const confidence = Math.round(probability * 10000) / 100;
          this.result = `Ovaj sadržaj ${isHate ? 'je' : 'nije'} govor mržnje. Model je ${confidence}% siguran.`;
        },
        error: (err) => {
          this.isloading = false
          console.error('error', err);
          this.result = "Došlo je do greške. Pokušajte ponovo.";
        },
      });
    } else if (this.selectedInput == '4') {
      this.imageUploadService.uploadFile(this.imageFile).subscribe({
        next: (response) => {
          this.isloading = false
          console.log('success', response);
          const { isHate, probability } = response;
          const confidence = Math.round(probability * 10000) / 100;
          this.result = `Ovaj sadržaj ${isHate ? 'je' : 'nije'} govor mržnje. Model je ${confidence}% siguran.`;
        },
        error: (err) => {
          this.isloading = false
          console.error('error', err);
          this.result = "Došlo je do greške. Pokušajte ponovo.";
        },
      });
     
    } else {
      this.isloading = false
      alert('Error!');
    }
    
  
  
  }
  onSubmit(){

  }
  selectChange(){
    this.result = null;
    
  }
}
