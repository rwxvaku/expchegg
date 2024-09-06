"""Constants for the expchegg integration."""

DOMAIN = "expchegg"

GRAPHQL_URL = "https://gateway.chegg.com/nestor-graph/graphql"

QUERY_NEXT_QC = """query GetNextQcAssignmentWithRetry {
  nextQcAssignmentWithRetry {
    assignmentId
    qcContentSource
    content {
      ... on Answer {
        id
        uuid
        headline
        isStructuredAnswer
        template {
          id
          __typename
        }
        answeredDate
        body
        author {
          id
          email
          uuid
          __typename
        }
        isDeleted
        question {
          questionTemplate {
            templateName
            templateId
            __typename
          }
          isDeleted
          author {
            email
            id
            __typename
          }
          createdDate
          id
          uuid
          body
          title
          subject {
            name
            id
            subjectGroup {
              id
              __typename
            }
            __typename
          }
          imageTranscriptionText
          subjectClassification {
            subSubjects {
              isTagRecommended
              subSubject {
                displayName
                name
                uuid
                __typename
              }
              __typename
            }
            topics {
              isTagRecommended
              topic {
                displayName
                name
                uuid
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      ... on PracticeAnswer {
        id
        uuid
        headline
        isStructuredAnswer
        template {
          id
          __typename
        }
        answeredDate
        body
        author {
          id
          email
          uuid
          __typename
        }
        isDeleted
        question {
          questionTemplate {
            templateName
            templateId
            __typename
          }
          isDeleted
          author {
            email
            id
            __typename
          }
          createdDate
          id
          uuid
          body
          title
          subject {
            name
            id
            subjectGroup {
              id
              __typename
            }
            __typename
          }
          imageTranscriptionText
          subjectClassification {
            subSubjects {
              isTagRecommended
              subSubject {
                displayName
                name
                uuid
                __typename
              }
              __typename
            }
            topics {
              isTagRecommended
              topic {
                displayName
                name
                uuid
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      ... on RecommendedSolution {
        uuid
        __typename
        body
        solutionCreatedDate
        author {
          id
          email
          uuid
          __typename
        }
        template {
          id
          name
          __typename
        }
        question {
          questionTemplate {
            templateName
            templateId
            __typename
          }
          isDeleted
          author {
            email
            id
            __typename
          }
          createdDate
          id
          uuid
          body
          title
          subject {
            name
            id
            subjectGroup {
              id
              __typename
            }
            __typename
          }
          imageTranscriptionText
          subjectClassification {
            subSubjects {
              isTagRecommended
              subSubject {
                displayName
                name
                uuid
                __typename
              }
              __typename
            }
            topics {
              isTagRecommended
              topic {
                displayName
                name
                uuid
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }
      }
      __typename
    }
    qcQuestionSubjectGroup {
      id
      __typename
    }
    isTranslated
    reviewerLanguage
    contentLanguage
    __typename
  }
}"""

QUERY_NEXT_QC_DATA = {
  "operationName": "GetNextQcAssignmentWithRetry",
  "variables": {},
  "query": QUERY_NEXT_QC
}

QUERY_USER_INFO = """query userinfo {
  me {
    id
    uuid
    email
    firstName
    lastName
    roles
    gender
    imageLink
    nickname
    createdDate
    expertProfile {
      name
      showTnc
      lastActiveSession
      hasExpertAuthoredBefore
      isStructuredAuthoringExperimentEnabled
      subjectGroupsAssigned {
        id
        name
        __typename
      }
      subSubjectsAssigned {
        name
        __typename
      }
      isStructuredAuthoringExperimentEnabled
      isSkipExperimentEnabled
      qualityFactor
      __typename
    }
    __typename
  }
}"""

QUERY_USER_INFO_DATA = {
    "operationName": "userinfo",
    "variables": {},
    "query": QUERY_USER_INFO
}