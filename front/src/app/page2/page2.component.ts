import { Component } from '@angular/core';
import { TweetService } from '../tweet.service';
import { NgFor } from '@angular/common';
import { MatTableModule } from '@angular/material/table';

@Component({
  selector: 'page2',
  imports: [MatTableModule, NgFor],
  templateUrl: './page2.component.html',
  styleUrl: './page2.component.css',
})
export class Page2Component {
  displayedColumns: string[] = ['account', 'reports', 'link'];
  dataSource:{username:string, counter:number}[] = [
    {username:"apolon12", counter:6}, {username:"boki56", counter:3}, {username:"slavicaaa", counter:2} 
  ];
  
  tweets: any[] = [];
  constructor(private tweetService: TweetService){}
  ngOnInit(): void {
    this.tweetService.getTweets().subscribe((data) => {
      //console.log(data)
      
      //this.dataSource = data
      
    });
  }
}
