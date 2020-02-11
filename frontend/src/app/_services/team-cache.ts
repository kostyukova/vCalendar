import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { TeamService } from '../api_client/api/team.service';
import { Team } from '../api_client/model/team';

@Injectable()
export class TeamCache {
  private subject: BehaviorSubject<Map<number, string>> = new BehaviorSubject(new Map());
  constructor(private apiClient: TeamService) {
    this.reload();
  }

  reload() {
    this.apiClient.findTeamBy()

      .subscribe((data: Team[]) =>
        this.subject.next(new Map<number, string>(data.map(x => [x.team_id, x.name]))
        ));
  }

  getFoundList(): Observable<Map<number, string>> {
    return this.subject.asObservable();
  }
}
