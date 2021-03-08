# coding=utf-8

"""
JSONMovieAgent
"""

from utils import Mediafile, open_file, load_json_metadata
from logging import PlexLogAdapter as log

# PLEX API
preferences = Prefs
load_file = Core.storage.load
PlexAgent = Agent.Movies
MediaProxy = Proxy.Media
Metadata = MetadataSearchResult
Trailer = TrailerObject


class JSONAgent(PlexAgent):
    """
    A Plex Metadata Agent for Movies.

    Uses JSON files as the metadata source for Plex Movies.
    """
    name = 'JSONAgent'
    ver = '0.0.1'
    primary_provider = True
    languages = [Locale.Language.NoLanguage]
    accepts_from = [
        'com.plexapp.agents.localmedia',
        'com.plexapp.agents.opensubtitles',
        'com.plexapp.agents.podnapisi',
        'com.plexapp.agents.subzero'
    ]
    contributes_to = [
        'com.plexapp.agents.themoviedb',
        'com.plexapp.agents.imdb',
        'com.plexapp.agents.none'
    ]

    # search function
    def search(self, results, media, lang):
        log.debug('# Invoking search function')

        log.info('{plugin} Version: {number}'.format(
            plugin=self.name, number=self.ver))
        log.debug('Plex Server Version: {number}'.format(
            number=Platform.ServerVersion))

        if preferences['debug']:
            log.info('Agent debug logging is enabled!')
        else:
            log.info('Agent debug logging is disabled!')

        mediafile = Mediafile(media.items[0].parts[0].file)
        json_metadata = load_json_metadata(mediafile)

        # Title
        try:
            media.name = json_metadata.get('title')
        except Exception as e:
            log.info('ERROR: No \'title\' tag in JSON. Aborting!')
            log.debug('Exception: {name}'.format(name=e))
            return
        # ID
        try:
            id = json_metadata.get('id').strip()
        except:
            id = ''
            pass
        if len(id) > 2:
            media.id = id
            log.debug('ID from json: {id}'.format(id=media.id))
        else:
            # if movie id doesn't exist, create
            # one based on hash of title and year
            def ord3(x):
                return '%.3d' % ord(x)

            id = int(''.join(map(ord3, media.name + str(media.year))))
            id = str(abs(hash(int(id))))
            media.id = id
            log.debug('ID generated: {id}'.format(id=media.id))

        results.Append(Metadata(id=media.id, name=media.name, year=media.year, lang=lang, score=100))

        try:
            log.info('Found movie information in JSON file:'
                     ' title = {media.name},'
                     ' id = {media.id}'.format(media=media))
        except:
            pass

    # update function
    def update(self, metadata, media, lang):
        log.debug('# Invoking update function')

        log.info('{plugin} Version: {number}'.format(
            plugin=self.name, number=self.ver))
        log.debug('Plex Server Version: {number}'.format(
            number=Platform.ServerVersion))

        if preferences['debug']:
            log.info('Agent debug logging is enabled!')
        else:
            log.info('Agent debug logging is disabled!')

        mediafile = Mediafile(media.items[0].parts[0].file)
        json_metadata = load_json_metadata(mediafile)

        log.debug('metadata: {name}'.format(name=metadata))

        # Title
        if json_metadata.get('title'):
            log.debug('title found: {name}'.format(name=json_metadata.get('title')))
            metadata.title = json_metadata.get('title')
        else:
            log.info('ERROR: No \'title\' tag in JSON. Aborting!')
            return

        # Year
        if json_metadata.get('year'):
            log.debug('year found: {name}'.format(name=json_metadata.get('year')))
            metadata.year = int(json_metadata.get('year'))

        # Summary
        if json_metadata.get('summary'):
            log.debug('summary found: {name}'.format(name=json_metadata.get('summary')))
            metadata.summary = json_metadata.get('summary')

        # Studio
        if json_metadata.get('studio'):
            log.debug('studio found: {name}'.format(name=json_metadata.get('studio')))
            metadata.studio = json_metadata.get('studio')

        # Genre
        if json_metadata.get('genre'):
            try:
                metadata.genres.clear()
                for genre in json_metadata.get('genre'):
                    log.debug('genre found: {name}'.format(name=genre))
                    metadata.genres.add(genre)
            except:
                pass

        # Country.
        if json_metadata.get('country'):
            try:
                metadata.countries.clear()
                for country in json_metadata.get('country'):
                    country = country.replace('United States of America', 'USA')
                    log.debug('country found: {name}'.format(name=country))
                    metadata.countries.add(country)
            except:
                pass

        # Directors.
        if json_metadata.get('director'):
            try:
                metadata.directors.clear()
                for movie_director in json_metadata.get('director'):
                    director = metadata.directors.new()
                    log.debug('director found: {name}'.format(name=movie_director))
                    director.name = movie_director
            except:
                pass

        # Writers.
        if json_metadata.get('writer'):
            try:
                metadata.writers.clear()
                for movie_writer in json_metadata.get('writer'):
                    writer = metadata.writers.new()
                    log.debug('writer found: {name}'.format(name=movie_writer))
                    writer.name = movie_writer
            except:
                pass

        # Tagline.
        if json_metadata.get('tagline'):
            log.debug('tagline found: {name}'.format(name=json_metadata.get('tagline')))
            metadata.tagline = json_metadata.get('tagline')

        # Actors.
        if json_metadata.get('actor'):
            try:
                metadata.roles.clear()
                for movie_role in json_metadata.get('actor'):
                    role = metadata.roles.new()
                    if movie_role.get('role'):
                        role.role = movie_role.get('role')
                    role.name = movie_role.get('name')
                    log.debug('actor found: {name}, role found: {role}'.format(name=role.name, role=role.role))
            except:
                pass

        return metadata
