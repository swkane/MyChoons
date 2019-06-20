import soundcloud

class GenericProvider(object):
  def __init__(self, track):
    self.track = track
    self.provider = eval(track.provider + "Provider")

  def upload(self, file, title, description):
    return self.provider(self.track).upload(file, title, description)

  def retrieve(self):
    return self.provider(self.track).retrieve()

class SCProvider(object):
  def __init__(self, track):
    self.track = track

    # UNSAFE
    self.client = soundcloud.Client(client_id='YOUR CLIENT ID',
                                   client_secret='YOUR CLIENT SECRET',
                                   username='YOUR USERNAME',
                                   password='YOUR PASSWORD')

  def upload(self, file, title, description):
      track = self.client.post('/tracks', track={
        'title': title, 
        'description': description, 
        'asset_data': file
        })

      self.track.uploaded = True
      self.track.provider_id = track.id
      self.track.save()

      return self.retrieve()

  def retrieve(self):
    retrieved = self.client.get('/tracks/'+ str(self.track.provider_id))
    return self._build_track(retrieved)

  def _build_track(self, provider_data):
    return BuiltTrack(
      id = self.track.id,
      provider = self.track.provider,
      provider_id = provider_data.id,
      provider_artwork_url = provider_data.artwork_url,
      provider_title = provider_data.title,
      provider_description = provider_data.description,
      provider_permalink = provider_data.permalink_url,
      provider_created_at = provider_data.created_at,
      uploaded = self.track.uploaded,
      created_at = self.track.created_at
    )
  
  class BuiltTrack(object):
    def __init__(self, **kwargs):
      for field in ('id', 'provider',
      'provider_id', 'provider_artwork_url', 
                      'provider_title', 'provider_description',
                      'provider_permalink', 'provider_created_at', 
                      'uploaded', 'created_at'):
        setattr(self, field, kwargs.get(field, None))