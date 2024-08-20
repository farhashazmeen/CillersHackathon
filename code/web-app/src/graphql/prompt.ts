import { gql } from '@apollo/client';

export const PROMPT = gql`
  query testopenaiGet {
    getopenai { message }
  }
`;



