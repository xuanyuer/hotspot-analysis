# Hotspot Analysis Report

**Total files:** 45 | **Hotspots:** 12 (27%)

| File | Churn | Complexity | Hotspot | Commits | Authors |
|------|-------|------------|---------|---------|---------|
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/BcpGrantService.java | 100.0 | 100.0 | 100.0 | 21 | 4 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/SsoGrantService.java | 100.0 | 80.0 | 89.4 | 21 | 4 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/common/BaseGrantService.java | 73.3 | 100.0 | 85.6 | 12 | 3 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/RedisService.java | 53.3 | 80.0 | 65.3 | 9 | 3 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/ConcurrentLoginService.java | 100.0 | 40.0 | 63.2 | 19 | 6 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/AccessRenewService.java | 53.3 | 40.0 | 46.2 | 9 | 2 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/AccessSwitchService.java | 13.3 | 100.0 | 36.5 | 3 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/RevokeAccessService.java | 13.3 | 80.0 | 32.7 | 3 | 2 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/controller/AccessApiController.java | 40.0 | 20.0 | 28.3 | 7 | 1 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/adaptor/AuthAdaptorTest.java | 20.0 | 40.0 | 28.3 | 4 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/common/CookieUtils.java | 6.7 | 100.0 | 25.8 | 2 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/adaptor/EntitlementAdaptor.java | 13.3 | 20.0 | 16.3 | 3 | 1 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/adaptor/EntitlementAdaptorTest.java | 6.7 | 20.0 | 11.5 | 2 | 1 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/service/common/BaseGrantServiceTest.java | 6.7 | 20.0 | 11.5 | 2 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/KongHandlerApplication.java | 6.7 | 0.0 | 0.0 | 2 | 2 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/adaptor/AuthAdaptor.java | 46.7 | 0.0 | 0.0 | 8 | 2 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/adaptor/AuthAdaptorProperties.java | 6.7 | 0.0 | 0.0 | 2 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/adaptor/EntitlementAdaptorProperties.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/adaptor/PostInternalBcpVerificationAdapterProperties.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/adaptor/ProfileAdaptor.java | 40.0 | 0.0 | 0.0 | 7 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/adaptor/ProfileAdaptorProperties.java | 20.0 | 0.0 | 0.0 | 4 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/config/KafkaConfig.java | 6.7 | 0.0 | 0.0 | 2 | 2 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/config/RedisConfig.java | 0.0 | 20.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/config/RequestLoggingFilter.java | 0.0 | 60.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/config/WireMockConfig.java | 0.0 | 40.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/controller/GrantController.java | 80.0 | 0.0 | 0.0 | 13 | 3 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/controller/RevokeController.java | 6.7 | 0.0 | 0.0 | 2 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/model/dto/AccessTokenDto.java | 13.3 | 0.0 | 0.0 | 3 | 3 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/model/dto/ApiErrorResponse.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/common/ActivityLogUtils.java | 0.0 | 80.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/common/BoEventPublisher.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/service/common/StreamAdaptorBoEventPublisher.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/bo/kong/handler/util/Constants.java | 100.0 | 0.0 | 0.0 | 16 | 6 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/adaptor/ProfileAdaptorTest.java | 6.7 | 0.0 | 0.0 | 2 | 1 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/controller/AccessApiControllerTest.java | 13.3 | 0.0 | 0.0 | 3 | 1 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/controller/GrantControllerTest.java | 0.0 | 20.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/controller/RevokeControllerTest.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/service/AccessRenewServiceTest.java | 26.7 | 0.0 | 0.0 | 5 | 1 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/service/AccessSwitchServiceTest.java | 13.3 | 0.0 | 0.0 | 3 | 1 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/service/BcpGrantServiceTest.java | 60.0 | 0.0 | 0.0 | 10 | 3 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/service/ConcurrentLoginServiceTest.java | 33.3 | 0.0 | 0.0 | 6 | 2 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/service/RedisServiceTest.java | 0.0 | 20.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/service/RevokeAccessServiceTest.java | 20.0 | 0.0 | 0.0 | 4 | 2 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/service/SsoGrantServiceTest.java | 80.0 | 0.0 | 0.0 | 13 | 2 |
| src/test/java/jp/co/smbc/gcms/bo/kong/handler/service/common/CookieUtilsTest.java | 6.7 | 0.0 | 0.0 | 2 | 1 |
