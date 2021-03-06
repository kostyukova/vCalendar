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
import { ApiResponse } from './apiResponse';
import { ConflictDetail } from './conflictDetail';


export interface ApiResponseConflict { 
    code?: number;
    type?: string;
    message?: string;
    details?: Array<ConflictDetail>;
}
