import { Injectable } from '@angular/core';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable'; // Importar el plugin

@Injectable({
  providedIn: 'root'
})
export class ReportService {

  constructor() { }

  exportAsPDF() {
    const doc = new jsPDF('l', 'pt', 'letter');
    const resultsTable = document.querySelector('#results') as HTMLElement;

    // Copiar la tabla original
    const clonedTable = resultsTable.cloneNode(true) as HTMLElement;
    // Crea un div centrado, metele la tabla clonada y hazle CSS

    // Ajustar el tamaño de la tabla clonada para el PDF
    clonedTable.style.width = '8in';

    // Establecer el overflow para que el contenido adicional se desplace hacia abajo
    clonedTable.style.overflowY = 'auto';

    // Agregar la tabla clonada al documento PDF
    doc.html(clonedTable, {
      callback: (doc: jsPDF) => {
        doc.save('pdf-export.pdf');
      }
    });
  }


}
