import { Injectable } from '@angular/core';
import * as pdfMake from 'pdfmake/build/pdfmake';
import * as pdfFonts from 'pdfmake/build/vfs_fonts';
import { cities, ciudades, estados, estadosLlamada, formatDate } from '../app.component';

(pdfMake as any).vfs = pdfFonts.pdfMake.vfs;

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  constructor() { }

  async exportAsPDF(data: any = null) {
    // Define el contenido del encabezado
    const header = {
      text: 'Huevos de Yoshi', // Título del encabezado
      style: 'header' // Estilo CSS del encabezado
    };

    // Descargar la imagen y convertirla a formato base64
    const imageBase64 = await this.getImageAsBase64('assets/huevos.jpeg');

    if (!imageBase64) {
      console.error('Error: No se pudo cargar la imagen');
      return;
    }

    // Define la imagen del encabezado
    const image = {
      image: imageBase64,
      width: 100, // Ancho de la imagen
      alignment: 'center' // Alineación de la imagen
    };

    // Obtén la tabla HTML por su ID
    const table: any = document.getElementById('results');

    // Crea una matriz para almacenar los datos de la tabla
    const tableData: any = [];
    tableData.push(['Fecha de llamada', 'Origen', 'Destino', 'Duracion (seg.)', 'Estado', 'Ciudad'])
    // Obtén las filas de la tabla HTML excluyendo la primera fila de encabezados
    console.log(data)
    if (data) {
      data.forEach((row: any) => {
        tableData.push([formatDate(row.calldate), row.src, row.dst, row.billsec, String(estadosLlamada[row.disposition]), String(cities[row.branch])])
      });
    }
    else {
      const rows = table?.querySelectorAll('tr');
      const dataRows = Array.from(rows!).slice(1);

      // Itera sobre las filas de datos y extrae los datos de cada celda
      dataRows.forEach((row: any) => {
        const rowData: any = [];
        row.querySelectorAll('td').forEach((cell: any) => {
          rowData.push(cell.textContent || ''); // Añade el texto de la celda a la fila de datos
        });
        tableData.push(rowData); // Añade la fila de datos a la matriz de datos de la tabla
      });
    }

    // Define la definición de la tabla para pdfmake
    const tableDefinition = {
      table: {
        headerRows: 1,
        body: tableData,
      },
    };

    // Define los estilos para el documento
    const styles = {
      header: {
        fontSize: 18,
        bold: true,
        alignment: 'center',
        margin: [0, 0, 0, 20],
      },
    };

    // Define el contenido del documento con la tabla
    const documentDefinition: any = {
      content: [
        header,
        image, // Añade la imagen del encabezado
        { text: 'Reporte de Llamadas', style: 'header' },
        tableDefinition,
      ],
      styles: styles, // Referencia los estilos definidos
    };

    // Crea el PDF con el contenido definido
    const pdfDoc = pdfMake.createPdf(documentDefinition);

    // Abre el PDF en una nueva ventana
    pdfDoc.open();
  }


  async getImageAsBase64(url: string): Promise<string> {
    const response = await fetch(url);
    const blob = await response.blob();
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }
}
