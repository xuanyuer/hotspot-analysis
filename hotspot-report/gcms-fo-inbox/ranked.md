# Hotspot Analysis Report

**Total files:** 46 | **Hotspots:** 46 (100%)

| File | Churn | Complexity | Hotspot | Commits | Authors |
|------|-------|------------|---------|---------|---------|
| src/main/java/jp/co/smbc/gcms/channel/inbox/service/PostInboxRetrievalService.java | 70.6 | 100.0 | 84.0 | 6 | 3 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/service/MessageRetrievalService.java | 47.1 | 100.0 | 68.6 | 4 | 4 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/batch/step/StepBulkOperationConfig.java | 35.3 | 100.0 | 59.4 | 3 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/service/PostInboxDeleteService.java | 23.5 | 100.0 | 48.5 | 2 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/config/RedisConfig.java | 47.1 | 40.0 | 43.4 | 4 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/service/BulkOperationBatchService.java | 23.5 | 80.0 | 43.4 | 2 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/service/PostInboxReadService.java | 47.1 | 40.0 | 43.4 | 4 | 4 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/batch/listener/BulkOperationListener.java | 11.8 | 100.0 | 34.3 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/service/InternalInboxDeleteService.java | 11.8 | 80.0 | 30.7 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/service/PostInboxBulkProcessService.java | 11.8 | 80.0 | 30.7 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/InboxApplication.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/adaptor/ProfileAdaptor.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/adaptor/ProfileAdaptorProperties.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/batch/job/BulkOperationJobConfig.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/batch/step/FlowBulkOperationConfig.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/controller/InboxController.java | 100.0 | 0.0 | 0.0 | 16 | 8 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/model/dto/InboxBatchJobRequest.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/model/entity/UserInboxLocalizedMessageEntity.java | 0.0 | 0.0 | 0.0 | 0 | 0 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/model/entity/UserInboxMessageAttachmentEntity.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/model/entity/UserInboxMessageEntity.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/model/enums/CategoryEnum.java | 0.0 | 0.0 | 0.0 | 0 | 0 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/property/BulkOperationProperties.java | 23.5 | 0.0 | 0.0 | 2 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/property/InboxConfigProperties.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/repository/UserInboxLocalizedMessageRepository.java | 94.1 | 0.0 | 0.0 | 8 | 5 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/repository/UserInboxMessageAttachmentRepository.java | 23.5 | 0.0 | 0.0 | 2 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/repository/UserInboxMessageRepository.java | 100.0 | 0.0 | 0.0 | 11 | 7 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/service/GetInboxKeywordSuggestionsService.java | 0.0 | 0.0 | 0.0 | 0 | 0 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/service/InboxService.java | 58.8 | 0.0 | 0.0 | 5 | 3 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/service/PostInternalInboxSendService.java | 35.3 | 0.0 | 0.0 | 3 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/inbox/util/Constants.java | 94.1 | 0.0 | 0.0 | 8 | 5 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/adaptor/ProfileAdaptorPropertiesTest.java | 35.3 | 0.0 | 0.0 | 3 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/adaptor/ProfileAdaptorTest.java | 35.3 | 0.0 | 0.0 | 3 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/controller/InboxControllerTest.java | 100.0 | 0.0 | 0.0 | 15 | 8 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/model/enums/CategoryEnumTest.java | 35.3 | 0.0 | 0.0 | 3 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/repository/RepositoryIntegrationNote.java | 35.3 | 0.0 | 0.0 | 3 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/service/BulkOperationBatchServiceTest.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/service/GetInboxKeywordSuggestionsTest.java | 23.5 | 0.0 | 0.0 | 2 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/service/InboxServiceTest.java | 58.8 | 0.0 | 0.0 | 5 | 3 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/service/InternalInboxDeleteServiceTest.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/service/MessageRetrievalServiceTest.java | 47.1 | 0.0 | 0.0 | 4 | 4 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/service/PostInboxBulkProcessServiceTest.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/service/PostInboxDeleteServiceTest.java | 11.8 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/service/PostInboxReadServiceTest.java | 35.3 | 0.0 | 0.0 | 3 | 3 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/service/PostInboxRetrievalServiceTest.java | 47.1 | 0.0 | 0.0 | 4 | 2 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/service/PostInternalInboxSendServiceTest.java | 35.3 | 0.0 | 0.0 | 3 | 2 |
| src/test/java/jp/co/smbc/gcms/channel/inbox/util/ConstantsTest.java | 35.3 | 0.0 | 0.0 | 3 | 1 |
