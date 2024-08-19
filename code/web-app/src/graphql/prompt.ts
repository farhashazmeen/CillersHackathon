import { gql } from '@apollo/client';

export const ITEMS = gql`
  query testopenaiGet {
    getopenai { message }
  }
`;



