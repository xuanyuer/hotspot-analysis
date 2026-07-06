# Hotspot Analysis Report

**Total files:** 34 | **Hotspots:** 34 (100%)

| File | Churn | Complexity | Hotspot | Commits | Authors |
|------|-------|------------|---------|---------|---------|
| src/main/java/jp/co/smbc/gcms/channel/push/notification/adaptor/FirebaseMessagingAdaptor.java | 100.0 | 100.0 | 100.0 | 12 | 4 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/config/FirebaseMessagingConfiguration.java | 100.0 | 100.0 | 100.0 | 10 | 5 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/service/NotificationService.java | 100.0 | 100.0 | 100.0 | 12 | 4 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/service/SseSubscriptionService.java | 29.1 | 100.0 | 53.9 | 3 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/properties/NotificationTemplateProperties.java | 29.1 | 40.0 | 34.1 | 3 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/adaptor/FirebaseMessagingAdaptorTest.java | 29.1 | 40.0 | 34.1 | 3 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/config/RedisConfig.java | 14.5 | 40.0 | 24.1 | 2 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/PushNotificationApplication.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/adaptor/NotificationAdaptorProperties.java | 43.6 | 0.0 | 0.0 | 4 | 3 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/adaptor/VaultProperties.java | 14.5 | 0.0 | 0.0 | 2 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/config/SseEmitterProperties.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/controller/NotificationController.java | 87.3 | 0.0 | 0.0 | 7 | 4 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/controller/SseSubscriptionController.java | 14.5 | 0.0 | 0.0 | 2 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/model/NotificationTemplateDto.java | 29.1 | 0.0 | 0.0 | 3 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/model/PushNotificationDetails.java | 29.1 | 0.0 | 0.0 | 3 | 3 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/model/PushNotificationEventDetails.java | 43.6 | 0.0 | 0.0 | 4 | 3 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/model/PushNotificationRecipient.java | 14.5 | 0.0 | 0.0 | 2 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/model/ServiceAccountCredential.java | 14.5 | 0.0 | 0.0 | 2 | 2 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/service/StreamPushNotificationProcessorService.java | 14.5 | 0.0 | 0.0 | 2 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/stream/PushNotificationConsumer.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/main/java/jp/co/smbc/gcms/channel/push/notification/util/Constants.java | 100.0 | 0.0 | 0.0 | 9 | 4 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/adaptor/NotificationAdaptorPropertiesTest.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/adaptor/VaultPropertiesTest.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/config/FirebaseMessagingConfigurationTest.java | 0.0 | 40.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/config/RedisConfigTest.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/config/SseEmitterPropertiesTest.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/controller/NotificationControllerTest.java | 29.1 | 0.0 | 0.0 | 3 | 2 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/controller/SseSubscriptionControllerTest.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/properties/NotificationTemplatePropertiesTest.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/service/NotificationServiceTest.java | 100.0 | 0.0 | 0.0 | 10 | 3 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/service/SseSubscriptionServiceTest.java | 29.1 | 0.0 | 0.0 | 3 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/service/StreamPushNotificationProcessorServiceTest.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/stream/PushNotificationConsumerTest.java | 0.0 | 0.0 | 0.0 | 1 | 1 |
| src/test/java/jp/co/smbc/gcms/channel/push/notification/util/ConstantsTest.java | 43.6 | 0.0 | 0.0 | 4 | 2 |
