FROM apache/nifi:latest

COPY nifi-esp-nar-5.2.nar /opt/nifi/nifi-current/lib
COPY nifi_rpg_game_demo_flow.xml /opt/nifi/nifi-current/conf
COPY --chown=nifi:nifi flow.xml.gz /opt/nifi/nifi-current/conf/

ADD --chown=nifi:nifi https://jdbc.postgresql.org/download/postgresql-42.2.5.jar /opt/nifi/nifi-current/lib/
