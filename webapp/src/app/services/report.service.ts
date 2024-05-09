import { Injectable } from '@angular/core';
import * as pdfMake from 'pdfmake/build/pdfmake';
import * as pdfFonts from 'pdfmake/build/vfs_fonts';
import { estadosLlamada, cities } from '../environment/utils'
import { formatDate } from '../app.component';
(pdfMake as any).vfs = pdfFonts.pdfMake.vfs;

@Injectable({
  providedIn: 'root'
})
export class ReportService {

  constructor() { }

  async exportAsPDF(data: any) {
    // Descargar la imagen y convertirla a formato base64
    const imageBase64 = await this.getImageAsBase64(
      'https://media.licdn.com/dms/image/C560BAQEOT91z8HuBEw/company-logo_200_200/0/1630641472142/granjas_avicolas_rancho_grande_logo?e=2147483647&v=beta&t=rj44v6tEdF5FbWLQMMjJlvlFKron7SuCrmacKypJ8XA');

    if (!imageBase64) {
      console.error('Error: No se pudo cargar la imagen');
      return;
    }

    // Define la imagen del encabezado
    const image = {
      image: imageBase64,
      width: 100, // Ancho de la imagen
      alignment: 'center', // Alineación de la imagen
      verticalAlign: 'top' // Alineación vertical hacia arriba
    };

    // Título del reporte
    const reportTitle = {
      text: 'Reporte de Llamadas',
      style: 'header',
      alignment: 'center',
      margin: [0, 0, 0, 20] // Margen inferior
    };

    // Nombre de la empresa
    const companyName = {
      text: 'EvieLand',
      alignment: 'center',
      verticalAlign: 'top' // Alineación vertical hacia arriba
    };

    // Fecha
    const currentDate = {
      text: '22 de mayo',
      alignment: 'center',
      verticalAlign: 'top' // Alineación vertical hacia arriba
    };

    // Encabezado
    const header = {
      columns: [
        image,
        companyName,
        currentDate
      ],
      margin: [0, 0, 0, 20] // Margen inferior
    };

    // Obtén la tabla HTML por su ID
    const table: any = document.getElementById('results');

    // Crea una matriz para almacenar los datos de la tabla
    const tableData: any = [];

    // Obtén las filas de la tabla HTML excluyendo la primera fila de encabezados
    const rows = table?.querySelectorAll('tr');
    const dataRows = Array.from(rows!).slice(1);
    tableData.push(['#', 'Fecha de llamada', 'Origen', 'Destino', 'Duración', 'Estado', 'Ciudad'])
    let id: any = 1
    data.forEach((row: any) => {
      tableData.push([
        id, formatDate(row.calldate),
        row.src,
        row.dst,
        row.billsec,
        estadosLlamada[row.disposition] || "NA",
        cities[row.branch]])
      id++;
    });

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
        bold: true, // Establece el estilo en negrita
        alignment: 'center',
        margin: [0, 0, 0, 20],
      },
    };

    // Define el contenido del documento
    const documentDefinition: any = {
      content: [
        header, // Añade el encabezado
        reportTitle, // Añade el título del reporte
        tableDefinition, // Añade la tabla
      ],
      styles: styles // Referencia los estilos definidos
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
