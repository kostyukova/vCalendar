import { Pipe, PipeTransform } from '@angular/core';
import { TeamCache } from './team-cache';


@Pipe({ name: 'teamname' })
export class TeamPipe implements PipeTransform {
  private teamName: string;
  constructor(private cache: TeamCache) { }

  transform(value: number, ...args: any[]): string {
    this.cache.getFoundList().subscribe((data: Map<number, string>) => {
      this.teamName = data.get(value);
    });
    return this.teamName;
  }
}
