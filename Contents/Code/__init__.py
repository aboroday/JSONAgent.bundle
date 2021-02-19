# coding=utf-8

"""
JSONMovieAgent
"""

from utils import Mediafile, open_file
from logging import PlexLogAdapter as log
import os
import json

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

        json_path = os.path.join(mediafile.folder, '{file}.json'.format(file = mediafile.filename))
        log.debug('loading JSON: {name}'.format(name=json_path))

        if os.path.exists(json_path):
            try:
                json_string = load_file(json_path)
                log.debug('JSON read:  {name}'.format(name=json_string))
                json_metadata = json.loads(json_string)
                log.debug('Metadata loaded from JSON:  {name}'.format(name=json_metadata))
            except Exception as e:
                log.debug('Metadata load failed:  {name}'.format(name=e))
        # Title
        try:
            media.name = json_metadata.get('title')
        except Exception as e:
            log.info('ERROR: No \'title\' tag in JSON. Aborting!')
            log.debug('Exception: {name}'.format(name=e))
            return
        # Sort Title
        try:
            media.title_sort = json_metadata.get('title_sort')
        except:
            log.info('WARNING: No \'title_sort\' tag in JSON.')
            pass
        # Year
        try:
            media.year = int(json_metadata.get('year').strip())
            log.debug('Reading year tag: {year}'.format(year=media.year))
        except:
            log.debug('WARNING: No \'year\' tag in JSON.')
            pass
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
                     ' year = {media.year},'
                     ' id = {media.id}'.format(media=media))
        except:
            pass

    # update function
    def update(self, metadata, media, lang):
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
        log.debug('full path: {name}'.format(name=mediafile.path))
        log.debug('folder path: {name}'.format(name=mediafile.folder))
        log.debug('media file: {name}'.format(name=mediafile.filename))
        log.debug('file name: {name}'.format(name=mediafile.file))
        log.debug('file ext: {name}'.format(name=mediafile.ext))

        json_path = os.path.join(mediafile.folder, '{file}.json'.format(file=mediafile.filename))
        log.debug('loading JSON: {name}'.format(name=json_path))

        if os.path.exists(json_path):
            try:
                json_string = load_file(json_path)
                log.debug('JSON read:  {name}'.format(name=json_string))
                json_metadata = json.loads(json_string)
                log.debug('Metadata loaded from JSON:  {name}'.format(name=json_metadata))
            except Exception as e:
                log.debug('Metadata load failed:  {name}'.format(name=e))

        log.debug('metadata: {name}'.format(name=metadata))

        # Title
        try:
            metadata.title = json_metadata.get('title')
        except Exception as e:
            log.info('ERROR: No \'title\' tag in JSON. Aborting!')
            log.debug('Exception: {name}'.format(name=e))
            return
        # Year
        try:
            metadata.year = int(json_metadata.get('year').strip())
            log.debug('Reading year tag: {year}'.format(year=metadata.year))
        except Exception as e:
            log.debug('WARNING: No \'year\' tag in JSON.')
            log.debug('Exception: {name}'.format(name=e))
            pass

        return metadata
