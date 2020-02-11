import { Pipe, PipeTransform } from '@angular/core';
import { Team } from '../api_client/model/team';
import { TeamCache } from './team-cache';


@Pipe({ name: 'teamname', pure: false })
export class TeamPipe implements PipeTransform {
  private teamName: string;
  constructor(private cache: TeamCache) {

  }

  transform(value: number, ...args: any[]): string {
    this.cache.getFoundList().subscribe((data: Map<number, string>) => {
      this.teamName = data.get(value);
      console.log(this.teamName, value);
    });
    return this.teamName;
  }
}
