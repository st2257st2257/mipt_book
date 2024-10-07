export interface IInstitute {
    name: string;
    description: string;
}

export interface IBuilding {
    name: string;
    institute: IInstitute;
    description: string;
}

export interface IAudienceStatus {
    name: string;
    description: string;
}

export interface IAudience {
    number: string;
    building: IBuilding;
    status: IAudienceStatus;
    number_of_users: number;
    description: string;
}

