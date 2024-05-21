import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { addr } from '../environment/env';

const ip = addr;

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) {}

  getCalls(data:any): Observable<any[]> {
    const url = `${ip}/calls_d?c=${data.c}&d=${data.d}&e=${data.e}&d1=${data.d1}&d2=${data.d2}&src=${data.src}&dst=${data.dst}`;
    return this.http.get<any[]>(url);
  }
}
