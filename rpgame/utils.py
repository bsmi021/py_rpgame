import datetime
import json
import uuid

import avro.schema
import pytz
from confluent_kafka.cimpl import Producer


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def get_localized_time():
    """ returns the timestamp of the attack"""
    utc_time = datetime.datetime.utcnow()
    return pytz.utc.localize(utc_time).astimezone()


def return_0_if_none(value_check):
    """ General function to return 0 if an int is null """
    if value_check is None or value_check is '':
        return 0
    else:
        return value_check


def kafka_producer_report(err, msg):
    """ Default response message when sending a message to kafka"""
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


def kafka_produce_message(producer: Producer, topic: str, message: str):
    """ Sends a message to Kafka"""
    producer.produce(topic, message.rstrip('\n').strip().encode('utf-8'), callback=kafka_producer_report)


def kafka_get_producer():
    return Producer({'bootstrap.servers': kafka_bootstrap_server})


kafka_bootstrap_server = '10.104.87.86'
party_topic = 'rpggame_parties'
player_topic = 'rpggame_players'
fight_topic = 'rpggame_fights'
attack_topic = 'rpggame_attacks'
enemy_topic = 'rpggame_enemies'


def get_avro_schema_from_json(json_string: str = None) -> str:
    avro.schema.Parse(json_string)
