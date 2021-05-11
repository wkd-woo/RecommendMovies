
# DB 라우터


class MultiDBRouter:
    def db_for_rating(self, model, **hints): # ratings가 필요할 때
        """
        rating 데이터를 가져와야 하는 경우, rating_db로 중계.
        """
        if model._meta.app_label == 'rating_data':
            return 'rating_db' # rating_data 로 DB 설정
        return None

    def allow_relation_with_rating(self, obj1, obj2, **hints):
        """
        rating과 관련된 관계 접근 허용
        """
        if obj1._meta.app_label == 'rating_data':
            return 'rating_db' # rating_data 로 DB 설정
        return None


    def db_for_genome(self, model, **hints): # genomes가 필요할 때
        """
        genome 데이터를 가져와야 하는 경우, genome_db로 중계.
        """
        if model._meta.app_label == 'genome_data':
            return 'genome_db' #genome_data 로 DB 설정
        return None

    def allow_relation_with_genome(self, obj1, obj2, **hints):
        """
        genome과 관련된 관계 접근 허용
        """
        if obj1._meta.app_label == 'genome_data':
            return 'genome_db' #genome_data 로 DB 설정
        return None


