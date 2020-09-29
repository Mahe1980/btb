
class Source(object):

    def __init__(self,
                 scope,
                 source_name,
                 source_type,
                 db_type,
                 load_type,
                 frequency,
                 state,
                 status,
                 batch_size,
                 parallelize,
                 watermark_columns,
                 value,
                 select_fields,
                 where_filter,
                 last_success_ts,
                 last_run_ts
                 ):
        self.scope = scope
        self.source_name = source_name
        self.source_type = source_type
        self.db_type = db_type
        self.load_type = load_type
        self.frequency = frequency
        self.state = state
        self.status = status
        self.chunk_size = batch_size
        self.parallelize = parallelize
        self.watermark_columns = watermark_columns
        self.value = value
        self.select_fields = select_fields
        self.where_filter = where_filter
        self.last_success_ts = last_success_ts
        self.last_run_ts = last_run_ts

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))

        return ', '.join(sb)
