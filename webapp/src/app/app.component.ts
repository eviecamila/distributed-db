import { Component } from '@angular/core';
import { ApiService } from './services/api.service';
import { ReportService } from './services/report.service';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})



export class AppComponent {
  cities: any = {
    M: 'Los Mochis',
    N: 'Navojoa',
    O: 'Obregon'
  }

  title = 'webapp';

  results = false;
  calls: any = []


  fechaInicio: string = ''
  fechaFin: string = ''

  filtro: string = '';
  ciudad: string = '';
  estadoLlamada: string = '';
  estados = [
    { value: 'A', status: 'Contestada' },
    { value: 'B', status: 'Ocupado' },
    { value: 'N', status: 'Sin Respuesta' },
    { value: 'F', status: 'Fallida' }
  ];
  ciudades = [
    { value: 'M', name: 'Mochis' },
    { value: 'N', name: 'Navojoa' },
    { value: 'O', name: 'Obregon' }
  ];

  constructor(private api: ApiService, private PDF: ReportService) { }

  ngOnInit(): void {
  }

  buscar() {
    // Llama al método buscar() de ApiService
    console.log(this.fechaFin, this.fechaInicio)
    this.api.getCalls({
      d: '', c: this.ciudad, e: this.estadoLlamada, d1: this.fechaInicio, d2: this.fechaFin
    }).subscribe((data: any) => {
      this.results = true;
      this.calls = data;
      console.log(data)
    });
  }
  generarReporte() {
    // Llama al método buscar() de ApiService
    console.log(this.fechaFin, this.fechaInicio)
    this.api.getCalls({
      d: '', c: this.ciudad, e: this.estadoLlamada, d1: this.fechaInicio, d2: this.fechaFin
    }).subscribe((data: any) => {
      this.PDF.exportAsPDF(); // Pasar los datos de la tabla a exportAsPDF()
    });
  }

}
