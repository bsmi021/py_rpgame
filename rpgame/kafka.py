import confluent_kafka


def produce_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


if __name__ == '__main__':
    producer = confluent_kafka.Producer({'bootstrap.servers': '18.235.75.135'})
    kafka_topic: str = 'rpggame2_combat_log'

    with open('..\data\combat_log.out', 'r') as log_file:
        for line in log_file:
            line = line.rstrip('\n') # remove line return

            kafka_message = line
            producer.produce(kafka_topic, kafka_message.encode('utf-8'), callback=produce_report)

    producer.flush()
