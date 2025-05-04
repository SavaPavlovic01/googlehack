import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TweetService {

  private apiUrl = 'http://localhost:8000/tweets/get'; // Change port if needed

  constructor(private http: HttpClient) {}

  getTweets(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}
