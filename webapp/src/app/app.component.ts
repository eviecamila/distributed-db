import { Component } from '@angular/core';
import { ApiService } from './services/api.service';
import { ReportService } from './services/report.service';
import { estadosLlamada, estados, ciudades, cities} from './environment/utils';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {


  title = 'webapp';

  results = false;
  calls: any = []


  fechaInicio: string = ''
  fechaFin: string = ''

  filtro: string = '';
  ciudad: string = '';
  estadoLlamada: string = '';

  ciudades = ciudades
  estadosLlamada=estadosLlamada
  estados=estados;cities=cities;
  constructor(private api: ApiService, private PDF: ReportService) { }

  ngOnInit(): void {
  }

  buscar() {
    // Llama al método buscar() de ApiService
    console.log(this.fechaFin, this.fechaInicio)
    let _Num = 1
    this.api.getCalls({
      d: '', c: this.ciudad, e: this.estadoLlamada, d1: this.fechaInicio, d2: this.fechaFin
    }).subscribe((data: any) => {
      // Formatea las fechas antes de asignar los datos a this.calls
      this.results = true;
      this.calls = data.map((call: any) => {
        // Formatea las fechas utilizando la función de formateo
        call.calldate = formatDate(call.calldate);
        call.number = _Num;
        _Num+=1
        return call;
      });
      console.log(data)
    });
  }
  generarReporte() {
    // Llama al método buscar() de ApiService
    console.log(this.fechaFin, this.fechaInicio)
    this.api.getCalls({
      d: '', c: this.ciudad, e: this.estadoLlamada, d1: this.fechaInicio, d2: this.fechaFin
    }).subscribe((data: any) => {
      this.PDF.exportAsPDF(data); // Pasar los datos de la tabla a exportAsPDF()
    });
  }

}


export function formatDate(dateString: string): string {
    const fechaOriginal = new Date(dateString);
    const opcionesDeFormato:any = {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false // Para usar el formato de 24 horas
    };
    return fechaOriginal.toLocaleString('en-US', opcionesDeFormato);
  }
