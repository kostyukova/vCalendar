/**
 * Swagger Vacation calendar
 * This is Vacarion Calendar API description
 *
 * OpenAPI spec version: 1.0.0
 * Contact: w.kostyukova@gmail.com
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */


export interface Employee {
    employee_id?: number;
    full_name: string;
    /**
     * Employee position
     */
    position: Employee.PositionEnum;
    /**
     * Employee specialization, comma separated value form set(BA, OACI, O365, Core)
     */
    specialization?: string;
    team_id: number;
    expert: boolean;
    email: string;
}
export namespace Employee {
    export type PositionEnum = 'junior engineer' | 'senior engineer' | 'chief engineer' | 'team leader';
    export const PositionEnum = {
        JuniorEngineer: 'junior engineer' as PositionEnum,
        SeniorEngineer: 'senior engineer' as PositionEnum,
        ChiefEngineer: 'chief engineer' as PositionEnum,
        TeamLeader: 'team leader' as PositionEnum
    };
}
