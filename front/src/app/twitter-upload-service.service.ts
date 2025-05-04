import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TwitterUploadServiceService {
  private apiUrl = 'http://localhost:8000/';

  constructor() {}

  private http = inject(HttpClient);

  uploadFile(text: string): Observable<any> {
    const formData = new FormData();
    formData.append('text', text);

    return this.http.post(this.apiUrl+'twitter', formData);
  }

  readTweets():Observable<any> {
    return this.http.get(this.apiUrl+'tweets/get')
  }
}
