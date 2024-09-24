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


QUERY_QC_STATS = """query QcReviewAppData {
  myReviewedQcStats(durationFilter: LIFE_TIME) {
    noOfQcReviewed
    __typename
  }
  myQcScoreStats {
    qcAccuracyScore
    __typename
  }
}"""

QUERY_QC_STATS_DATA = {
    "operationName": "QcReviewAppData",
    "variables": {},
    "query": QUERY_QC_STATS
}

QUERY_NEXT_QA = """
query NextQuestionAnsweringAssignment {
  nextQuestionAnsweringAssignment {
    question {
      body
      id
      uuid
      subject {
        id
        name
        subjectGroup {
          id
          name
          __typename
        }
        __typename
      }
      imageTranscriptionText
      lastAnswerUuid
      questionTemplate {
        templateName
        templateId
        __typename
      }
      __typename
    }
    langTranslation {
      body
      translationLanguage
      __typename
    }
    legacyAnswer {
      id
      body
      isStructuredAnswer
      structuredBody
      template {
        id
        __typename
      }
      __typename
    }
    questionGeoLocation {
      countryCode
      countryName
      languages
      __typename
    }
    questionRoutingDetails {
      answeringStartTime
      bonusCount
      bonusTimeAllocationEnabled
      checkAnswerStructureEnabled
      hasAnsweringStarted
      questionAssignTime
      questionSolvingProbability
      routingType
      allocationExperimentId
      questionQualityFactor
      routingTag
      __typename
    }
    variant
    __typename
  }
}
"""


QUERY_NEXT_QA_DATA = {
    "operationName": "NextQuestionAnsweringAssignment",
    "variables": {},
    "query": QUERY_NEXT_QA
}