import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ImageUploadServiceService {
  private apiUrl = 'http://localhost:8000/image-to-text';

  constructor() {}

  private http = inject(HttpClient);

  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);

    return this.http.post(this.apiUrl, formData);
  }
}
