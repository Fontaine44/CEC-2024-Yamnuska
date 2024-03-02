import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-form',
  templateUrl: './algo4.component.html',
  styleUrls: ['./algo4.component.scss']
})
export class Algo4Component {
  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.getData();
  }

  getData(): void {
    const apiUrl = 'https://codecraft.tv/courses/angular/http/http-with-observables/';

    this.http.get(apiUrl).subscribe(
      (data) => {
        console.log('Data received:', data);
      },
      (error) => {
        console.error('Error:', error);
      }
    );
  }

  postData(): void {
    const apiUrl = 'https://jsonplaceholder.typicode.com/posts';
    const postData = {
      title: 'foo',
      body: 'bar',
      userId: 1
    };

    this.http.post(apiUrl, postData).subscribe(
      (data) => {
        console.log('Data posted successfully:', data);
      },
      (error) => {
        console.error('Error posting data:', error);
      }
    );
  }
  
}
