import { Pipe, PipeTransform } from '@angular/core';


@Pipe({ name: 'yesno' })
export class YesnoPipe implements PipeTransform {
  constructor() { }

  transform(value: boolean, ...args: any[]): string {
    return value ? 'Yes' : 'No';
  }
}
