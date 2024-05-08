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


  estados: any = [
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
  estadosLlamada: any = {
    ANSWERED: 'Contestada', BUSY: 'Ocupado', 'NO ANSWER': 'Sin Respuesta', 'FAILED': 'Fallida'
  }
  constructor(private api: ApiService, private PDF: ReportService) { }

  ngOnInit(): void {
  }

  buscar() {
    // Llama al método buscar() de ApiService
    console.log(this.fechaFin, this.fechaInicio)
    this.api.getCalls({
      d: '', c: this.ciudad, e: this.estadoLlamada, d1: this.fechaInicio, d2: this.fechaFin
    }).subscribe((data: any) => {
      // Formatea las fechas antes de asignar los datos a this.calls
      this.results = true;
      this.calls = data.map((call: any) => {
        // Formatea las fechas utilizando la función de formateo
        call.calldate = this.formatDate(call.calldate);
        return call;
      });
      console.log(data)
    });
  }

  formatDate(dateString: string): string {
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



  generarReporte() {
    // Llama al método buscar() de ApiService
    // console.log(this.fechaFin, this.fechaInicio)
    // this.api.getCalls({
    //   d: '', c: this.ciudad, e: this.estadoLlamada, d1: this.fechaInicio, d2: this.fechaFin
    // }).subscribe((data: any) => {
      this.PDF.exportAsPDF(); // Pasar los datos de la tabla a exportAsPDF()
    // });?
  }

}
