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
    // Ajustar el tamaño de la tabla clonada para el PDF
    clonedTable.style.width = '8in';
    // Establecer el overflow para que el contenido adicional se desplace hacia abajo
    clonedTable.style.overflowY = 'auto';
    const headers = clonedTable.children[0].innerHTML;
    const tableBody = clonedTable.children[1];
    const rows = tableBody.querySelectorAll('tr');

    const pageSize = doc.internal.pageSize;
    const pageHeight = pageSize.height || pageSize.getHeight();
    const headerHeight = this.getHeight(headers);
    const rowHeight = this.getHeight(rows[0].innerHTML);

    // Calcular cuántas filas caben en una página
    const rowCountPerPage = Math.floor((pageHeight - headerHeight) / rowHeight);

    // Dividir la tabla en partes que quepan completamente en cada página
    let startRow = 0;
    while (startRow < rows.length) {
      const endRow = Math.min(startRow + rowCountPerPage, rows.length);
      const tablePart = this.getTablePart(clonedTable, startRow, endRow);
      doc.html(tablePart.outerHTML, {
        callback: (doc: jsPDF) => {
          if (endRow < rows.length) {
            doc.addPage();
          } else {
            doc.save('pdf-export.pdf');
          }
        }
      });
      startRow = endRow;
    }
  }

  // Función para obtener la altura de un elemento HTML
  private getHeight(html: string): number {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    document.body.appendChild(tempDiv);
    const height = tempDiv.offsetHeight;
    document.body.removeChild(tempDiv);
    return height;
  }

  // Función para obtener una parte de la tabla
  private getTablePart(table: HTMLElement, startRow: number, endRow: number): HTMLElement {
    const part = table.cloneNode(true) as HTMLElement;
    const tableBody = part.children[1] as HTMLElement;
    while (tableBody.children.length > endRow - startRow) {
      const lastChild = tableBody.lastChild;
      if (lastChild) {
        tableBody.removeChild(lastChild);
      } else {
        break; // Salir del bucle si no hay más hijos
      }
    }
    return part;
  }


}
