# Hotspot Analysis Report

**Total files:** 41 | **Hotspots:** 11 (27%)

| File | Churn | Complexity | Hotspot | Commits | Authors |
|------|-------|------------|---------|---------|---------|
| src/main/java/com/gcms/fo/batch/processor/MT940ItemProcessor.java | 100.0 | 100.0 | 100.0 | 20 | 5 |
| src/main/java/com/gcms/fo/batch/reader/MT940FileItemReader.java | 100.0 | 100.0 | 100.0 | 43 | 9 |
| src/main/java/com/gcms/fo/service/FileManagementService.java | 63.6 | 100.0 | 79.8 | 7 | 3 |
| src/test/java/com/gcms/fo/service/FileManagementServiceTest.java | 81.8 | 60.0 | 70.1 | 9 | 3 |
| src/main/java/com/gcms/fo/batch/writer/MT940ItemWriter.java | 54.5 | 40.0 | 46.7 | 6 | 3 |
| src/test/java/com/gcms/fo/batch/reader/MT940FileItemReaderTest.java | 100.0 | 20.0 | 44.7 | 29 | 8 |
| src/main/java/com/gcms/fo/service/SmbFilePollerService.java | 90.9 | 20.0 | 42.6 | 10 | 4 |
| src/main/java/com/gcms/fo/controller/FileManagementController.java | 63.6 | 20.0 | 35.7 | 7 | 3 |
| src/main/java/com/gcms/fo/util/KafkaMessagePublisher.java | 45.5 | 20.0 | 30.2 | 5 | 3 |
| src/test/java/com/gcms/fo/config/WireMockConfigTest.java | 9.1 | 80.0 | 27.0 | 1 | 1 |
| src/main/java/com/gcms/fo/entity/MT940LikeRequestFileEntity.java | 9.1 | 60.0 | 23.4 | 1 | 1 |
| src/main/java/com/gcms/fo/adaptor/AccountAdaptor.java | 9.1 | 40.0 | 19.1 | 1 | 1 |
| src/main/java/com/gcms/fo/config/WireMockConfig.java | 9.1 | 40.0 | 19.1 | 1 | 1 |
| src/main/java/com/gcms/fo/AccountOnboardingApplication.java | 36.4 | 0.0 | 0.0 | 4 | 4 |
| src/main/java/com/gcms/fo/adaptor/AccountAdaptorProperties.java | 0.0 | 0.0 | 0.0 | 0 | 0 |
| src/main/java/com/gcms/fo/batch/config/MT940BatchJobConfig.java | 18.2 | 0.0 | 0.0 | 2 | 1 |
| src/main/java/com/gcms/fo/config/KafkaConfig.java | 0.0 | 0.0 | 0.0 | 0 | 0 |
| src/main/java/com/gcms/fo/config/SmbConfig.java | 54.5 | 0.0 | 0.0 | 6 | 3 |
| src/main/java/com/gcms/fo/dto/FileMoveRequest.java | 36.4 | 0.0 | 0.0 | 4 | 3 |
| src/main/java/com/gcms/fo/dto/FileMoveResponse.java | 27.3 | 0.0 | 0.0 | 3 | 2 |
| src/main/java/com/gcms/fo/dto/MT940Account.java | 18.2 | 0.0 | 0.0 | 2 | 2 |
| src/main/java/com/gcms/fo/dto/MT940DTO.java | 9.1 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/com/gcms/fo/dto/MT940Header.java | 9.1 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/com/gcms/fo/dto/MT940Transaction.java | 27.3 | 0.0 | 0.0 | 3 | 3 |
| src/main/java/com/gcms/fo/dto/PostAccountsSearchByInternalMappingRequest.java | 9.1 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/com/gcms/fo/dto/PostAccountsSearchByInternalMappingResponse.java | 9.1 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/com/gcms/fo/repository/MT940LikeRequestFileRepository.java | 45.5 | 0.0 | 0.0 | 5 | 3 |
| src/main/java/com/gcms/fo/util/BigDecimalProtoConverter.java | 0.0 | 20.0 | 0.0 | 0 | 0 |
| src/main/java/com/gcms/fo/util/Constants.java | 27.3 | 0.0 | 0.0 | 3 | 3 |
| src/main/java/com/gcms/fo/util/Mt940Type.java | 9.1 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/com/gcms/fo/util/StreamHeader.java | 0.0 | 0.0 | 0.0 | 0 | 0 |
| src/test/java/com/gcms/fo/adaptor/AccountAdaptorTest.java | 27.3 | 0.0 | 0.0 | 3 | 3 |
| src/test/java/com/gcms/fo/batch/config/MT940BatchJobConfigTest.java | 9.1 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/com/gcms/fo/batch/processor/MT940ItemProcessorTest.java | 45.5 | 0.0 | 0.0 | 5 | 4 |
| src/test/java/com/gcms/fo/batch/writer/MT940ItemWriterTest.java | 9.1 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/com/gcms/fo/config/KafkaConfigTest.java | 9.1 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/com/gcms/fo/controller/FileManagementControllerTest.java | 36.4 | 0.0 | 0.0 | 4 | 3 |
| src/test/java/com/gcms/fo/entity/MT940LikeRequestFileEntityTest.java | 27.3 | 0.0 | 0.0 | 3 | 3 |
| src/test/java/com/gcms/fo/repository/MT940LikeRequestFileRepositoryTest.java | 9.1 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/com/gcms/fo/service/SmbFilePollerServiceTest.java | 18.2 | 0.0 | 0.0 | 2 | 2 |
| src/test/java/com/gcms/fo/util/KafkaMessagePublisherTest.java | 9.1 | 0.0 | 0.0 | 1 | 1 |
