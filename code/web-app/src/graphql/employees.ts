import { gql } from '@apollo/client';

// Query to get all employees
export const EMPLOYEES = gql`
  query EmployeesGet {
    employees {
      id
      name
      availability
    }
  }
`;

// Mutation to create employees
export const EMPLOYEES_CREATE = gql`
  mutation EmployeeCreate($employees: [EmployeeCreateInput!]!) {
    employeesCreate(employees: $employees) {
      id
      name
      availability
    }
  }
`;

// Mutation to remove employees
export const EMPLOYEES_REMOVE = gql`
  mutation EmployeesRemove($ids: [String!]!) {
    employeesRemove(ids: $ids)
  }
`;

// Subscription to listen for new employees created
export const EMPLOYEES_CREATED = gql`
  subscription OnEmployeeCreated {
    employeesCreated {
      id
      name
      availability
    }
  }
`;