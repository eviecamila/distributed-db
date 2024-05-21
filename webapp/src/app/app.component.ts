import { Component } from '@angular/core';
import { ApiService } from './services/api.service';
import { ReportService } from './services/report.service';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})



export class AppComponent {

  currentPage = 1;
  pageSize = 10; // Define el tamaño de la página aquí
  nextPage() {
    if (this.currentPage * this.pageSize < this.calls.length) {
      this.currentPage++;
    }
  }

  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }
  title = 'webapp';

  results = false;
  calls: any[] = []

  fechaInicio: string = ''
  fechaFin: string = ''

  filtro: string = '';
  ciudad: string = '';

  origen: string = '';
  destino: string = '';
  estadoLlamada: string = '';





  constructor(private api: ApiService, private PDF: ReportService) { }

  ngOnInit(): void {
  }

  buscar() {
    // Llama al método buscar() de ApiService
    console.log(this.fechaFin, this.fechaInicio)
    this.api.getCalls({
      d: '', c: this.ciudad, e: this.estadoLlamada, d1: this.fechaInicio, d2: this.fechaFin,
      dst: this.destino, src: this.origen
    }).subscribe((data: any) => {
      // Formatea las fechas antes de asignar los datos a this.calls
      this.results = true;
      this.calls = data.map((call: any) => {
        // Formatea las fechas utilizando la función de formateo
        call.calldate = formatDate(call.calldate);
        return call;
      });
      // console.log(data)
    });
  }

  ciudades = ciudades; estados = estados
  estadosLlamada = estadosLlamada
  cities = cities


  generarReporte() {
    // Llama al método buscar() de ApiService
    // console.log(this.fechaFin, this.fechaInicio)
    this.api.getCalls({
      d: '', c: this.ciudad, e: this.estadoLlamada, d1: this.fechaInicio, d2: this.fechaFin,
      dst: this.destino, src: this.origen
    }).subscribe((data: any) => {
      this.PDF.exportAsPDF(data); // Pasar los datos de la tabla a exportAsPDF()
    });
  }

}


export function formatDate(dateString: any): any {
  const fechaOriginal = new Date(dateString);
  const opcionesDeFormato: Intl.DateTimeFormatOptions = {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false // Para usar el formato de 24 horas
  };
  return fechaOriginal.toLocaleString('en-US', opcionesDeFormato);
}


export const ciudades: any = [
  { value: 'M', name: 'Mochis' },
  { value: 'N', name: 'Navojoa' },
  { value: 'O', name: 'Obregon' }
];

export const estados = [
  { value: 'A', status: 'Contestada' },
  { value: 'B', status: 'Ocupado' },
  { value: 'N', status: 'Sin Respuesta' },
  { value: 'F', status: 'Fallida' }
];
export const estadosLlamada: any = {
  'ANSWERED': 'Contestada', 'BUSY': 'Ocupado', 'NO ANSWER': 'Sin Respuesta', 'FAILED': 'Fallida'
}

export const cities: any = {
  M: 'Los Mochis',
  N: 'Navojoa',
  O: 'Obregon'
}
